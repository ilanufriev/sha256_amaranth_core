#include <sha256.h>
#include <stdint.h>
#include <stdio.h>

static const uint32_t H_CONST[8] = {
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
};

static const uint32_t K_CONST[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

sha256_status_t sha256_pad_msg(const char *msg, const size_t msgsize,
                               const size_t totsize, char *padmsg,
                               size_t *padsize)
{
    size_t bits = totsize * 8;
    size_t tmpsize = 0;

    if (msg == NULL)
    {
        return SHA256_BAD_DATA_PTR;
    }

    if (padmsg == NULL)
    {
        return SHA256_BAD_DATA_PTR;
    }

    if (padsize == NULL)
    {
        return SHA256_BAD_DATA_PTR;
    }

    for (int i = 0; i < msgsize; i++)
    {
        padmsg[tmpsize] = msg[tmpsize];
        tmpsize += 1;
    }

    *padsize = msgsize + 56 - (msgsize & 63) + 8;
    if ((msgsize & 63) >= 56)
    {
        *padsize += 64;
    }

    padmsg[tmpsize++] = 0x80;

    while (tmpsize < (*padsize - 8))
    {
        padmsg[tmpsize++] = 0x00;
    }

    for (size_t i = 0; i < 8; i++)
    {
        padmsg[tmpsize++] = (bits >> ((7 - i) * 8)) & 0xFF;
    }

    return SHA256_OK;
}

sha256_status_t sha256_init(struct sha256_state *s)
{
    if (s == NULL)
    {
        return SHA256_BAD_STATE_PTR;
    }

    for (int i = 0; i < 8; i++)
    {
        s->h_[i] = H_CONST[i];
    }

    return SHA256_OK;
}

/*
 * Rotate given number to the right by "bits" bits.
 */
static uint32_t rotr32(const uint32_t x, const uint32_t bits)
{
    return (x >> bits) | (x << (32 - bits));
}

/*
 * Shift given number to the right by "bits" bits.
 *
 * This function exists for syntax uniformity between
 * rotation and shift operations.
 */
static uint32_t rshi32(const uint32_t x, const uint32_t bits)
{
    return x >> bits;
}

/*
 * Calculate new scheduling array value based on
 * current window of w-values.
 *
 * Params:
 * - w - array of 16 32-bit unsigned numbers.
 * Returns:
 * - new w value.
 *
 */
static uint32_t new_w(const uint32_t *w)
{
    uint32_t s0 = rotr32(w[1], 7) ^ rotr32(w[1], 18) ^ rshi32(w[1], 3);
    uint32_t s1 = rotr32(w[14], 17) ^ rotr32(w[14], 19) ^ rshi32(w[14], 10);
    return w[0] + s0 + w[9] + s1;
}

static uint32_t S1(const uint32_t e)
{
    return rotr32(e, 6) ^ rotr32(e, 11) ^ rotr32(e, 25);
}

static uint32_t ch(const uint32_t e, const uint32_t f, const uint32_t g)
{
    return (e & f) ^ ((~e) & g);
}

static uint32_t S0(const uint32_t a)
{
    return rotr32(a, 2) ^ rotr32(a, 13) ^ rotr32(a, 22);
}

static uint32_t maj(const uint32_t a, const uint32_t b, const uint32_t c)
{
    return (a & b) ^ (a & c) ^ (b & c);
}

sha256_status_t sha256_update(struct sha256_state *s,
                              const char *data)
{
    uint32_t w[16];
    uint32_t a, b, c, d, e, f, g, h;

    if (s == NULL)
    {
        return SHA256_BAD_STATE_PTR;
    }

    if (data == NULL)
    {
        return SHA256_BAD_DATA_PTR;
    }

    for (int i = 0; i < 16; i++)
    {
        w[i]  = 0;
        w[i] |= ((uint32_t) (data[i * 4 + 0] & 0xff)) << 24;
        w[i] |= ((uint32_t) (data[i * 4 + 1] & 0xff)) << 16;
        w[i] |= ((uint32_t) (data[i * 4 + 2] & 0xff)) << 8;
        w[i] |= ((uint32_t) (data[i * 4 + 3] & 0xff));
    }

    a = s->h_[0];
    b = s->h_[1];
    c = s->h_[2];
    d = s->h_[3];
    e = s->h_[4];
    f = s->h_[5];
    g = s->h_[6];
    h = s->h_[7];

    for (int i = 0; i < 64; i++)
    {
        uint32_t w_i = (i > 15) ? (new_w(w)) : w[0];

        uint32_t temp1 = h + S1(e) + ch(e, f, g) + K_CONST[i] + w_i;
        uint32_t temp2 = S0(a) + maj(a, b, c);

        /* Scrambling working variables */
        h = g;
        g = f;
        f = e;
        e = d + temp1;
        d = c;
        c = b;
        b = a;
        a = temp1 + temp2;

        /* Rotate schedule array window */
        for (int j = 0; j < 15; j++)
        {
            w[j] = w[j + 1];
        }

        w[15] = w_i;
    }

    /* Adding working variables to current hash value */
    s->h_[0] += a;
    s->h_[1] += b;
    s->h_[2] += c;
    s->h_[3] += d;
    s->h_[4] += e;
    s->h_[5] += f;
    s->h_[6] += g;
    s->h_[7] += h;

    return SHA256_OK;
}

sha256_status_t sha256_get_hash(struct sha256_state *s, char *hash)
{
    if (s == NULL)
    {
        return SHA256_BAD_STATE_PTR;
    }

    if (hash == NULL)
    {
        return SHA256_BAD_DATA_PTR;
    }

    int32_t global_b_idx = 0;
    for (int32_t h_idx = 7; h_idx >= 0; h_idx--)
    {
        for (int32_t b_idx = 0; b_idx < 4; b_idx++)
        {
            hash[global_b_idx++] = (s->h_[h_idx] >> (b_idx * 8)) & 0xff;
        }
    }

    return SHA256_OK;
}
