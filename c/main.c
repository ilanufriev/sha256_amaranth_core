#include <sha256.h>
#include <stdio.h>
#include <unistd.h>
#include <argp.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>

#define die_custom(msg) \
    do { fprintf(stderr, msg "\n"); exit(1); } while(0);
#define die(msg) \
    do { fprintf(stderr, msg ": %s\n", strerror(errno)); exit(errno); } while(0);

const char *argp_program_version = "sha256_cli 1.0";
const char *argp_program_bug_address = "<anufriewwi2@mail.ru>";

static const char doc[] = "sha256_cli - compute sha256 for a file or stdin";

static struct argp_option options[] = {
    { "file", 'f', "FILE", 0, "Compute hash for file instead of stdin." },
    { "little-endian", 'l', 0, 0, "Output hash in little-endian instead of big-endian." },
    { 0 },
};

struct arguments
{
    char *file;
    int   little_endian;
};

static error_t parse_opt(int key, char *arg, struct argp_state *state)
{
    struct arguments *args = state->input;

    switch (key)
    {
        case 'f':
            args->file = arg;
            break;
        case 'l':
            args->little_endian = 1;
            break;
        default:
            return ARGP_ERR_UNKNOWN;
    }

    return 0;
}

static struct argp argp = { options, parse_opt, NULL, doc };

void print_bytes(int fd, const char *bytes, const int64_t start, const int64_t end)
{
    if (start < end)
    {
        for (int i = start; i < end; i++)
        {
            dprintf(fd, "%02hhx", bytes[i]);
        }
    }
    else
    {
        for (int i = start; i >= end; i--)
        {
            dprintf(fd, "%02hhx", bytes[i]);
        }
    }
}

void println_bytes(int fd, const char *bytes, const int64_t start, const int64_t end)
{
    print_bytes(fd, bytes, start, end);
    dprintf(fd, "\n");
}

int run(struct arguments *args)
{
    int rc = 0;
    int fd = STDIN_FILENO;

    char hash[32];
    char rdbuf[64];
    char padbuf[128];

    size_t padsize = 0;
    size_t totsize = 0;

    struct sha256_state s;

    if (sha256_init(&s))
    {
        die_custom("Failed to initialize sha256 state");
    }

    if (args->file != NULL)
    {
        fd = open(args->file, O_RDONLY);
        if (fd < 0)
            die("Could not open given file");
    }

    while (1)
    {
        rc = read(fd, rdbuf, 64);
        if (rc < 0 && (rc == EINTR))
            continue;

        if (rc < 0)
            die("Error when reading fiven file")

        totsize += rc;

        if (rc == 0 || rc < 64)
            break;

        if (sha256_update(&s, rdbuf))
            die_custom("Failed to hash block of data");
    }

    sha256_pad_msg(rdbuf, rc, totsize, padbuf, &padsize);
    if (sha256_update(&s, padbuf))
        die_custom("Failed to hash block of data");

    if (padsize > 64)
    {
        if (sha256_update(&s, padbuf + 64))
            die_custom("Failed to hash block of data");
    }

    sha256_get_hash(&s, hash);
    if (args->little_endian)
    {
        println_bytes(STDOUT_FILENO, hash, 0, 32);
    }
    else
    {
        println_bytes(STDOUT_FILENO, hash, 31, 0);
    }

    return 0;
}


int main(int argc, char **argv)
{
    struct arguments args = {
        .file = NULL,
        .little_endian = 0,
    };

    argp_parse(&argp, argc, argv, 0, 0, &args);
    return run(&args);
}
