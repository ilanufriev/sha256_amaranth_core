#ifndef __SHA_256_H__
#define __SHA_256_H__

#include <stdint.h>
#include <stdlib.h>

struct sha256_state
{
    uint32_t h_[8];
};

typedef enum
{
    SHA256_OK = 0,
    SHA256_BAD_STATE_PTR = 1,
    SHA256_BAD_DATA_PTR = 2,
} sha256_status_t;

/*
 * Add padding to a message that is less than block size.
 *
 * Params:
 * - msg     - [in] message that will need to be padded.
 * - msgsize - size of this message in bytes.
 * - totsize - total size of all hashed data in bytes.
 * - padmsg  - [out] array of chars that will hold padded
 *             message. Must be at least 128 bytes long.
 * - padsize - [out] size of the padded msg.
 * Returns:
 * - status of the operation:
 *   - SHA256_BAD_DATA_PTR - pointer of the msg, padmsg or padsize is NULL or
 *     invalid in some other way.
 *   - SHA256_OK - operation completed just fine.
 */
sha256_status_t sha256_pad_msg(const char *msg, const size_t msgsize, const size_t totsize,
                               char *padmsg, size_t *padsize);
/*
 * Initialize the algorithm.
 *
 * Params:
 * - s    - [in] state of the algorithm. Must be preallocated.
 * - data - [in] first block of data to be hashed. Must be 64 bytes long.
 * Returns:
 * - status of the operation:
 *   - SHA256_BAD_STATE_PTR - pointer of the state is NULL or
 *     invalid in some other way.
 *   - SHA256_OK - operation completed just fine.
 */
sha256_status_t sha256_init(struct sha256_state *s);

/*
 * Update algorithm with new block of data.
 *
 * Params:
 * - s    - [in] state of the algorithm. Must be initialized.
 * - data - [in] block of data to be hashed. Must 64 bytes long.
 * Returns:
 * - status of the operation:
 *   - SHA256_BAD_STATE_PTR - pointer of the state is NULL or
 *     invalid in some other way.
 *   - SHA256_BAD_DATA_PTR - pointer of the data is NULL or
 *     invalid in some other way.
 *   - SHA256_OK - operation completed just fine.
 */
sha256_status_t sha256_update(struct sha256_state *s,
                              const char *data);
/*
 * Get hash from the state.
 *
 * Params:
 * - s    - [in] state of the algorithm. Must be initialized.
 * - hash - [out] pointer to array of chars of size 32.
 * Returns:
 * - status of the operation:
 *   - SHA256_BAD_STATE_PTR - pointer of the state is NULL or
 *     invalid in some other way.
 *   - SHA256_BAD_DATA_PTR - pointer of the hash is NULL or
 *     invalid in some other way.
 *   - SHA256_OK - operation completed just fine.
 */
sha256_status_t sha256_get_hash(struct sha256_state *s, char *hash);

#endif // __SHA_256_H__
