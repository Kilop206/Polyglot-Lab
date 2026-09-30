# Official Test Vectors

These vectors provide canonical wire examples shared by every language.

Each JSON file describes a case. Most cases have a sibling `.bin` file
containing the exact bytes.

A language implementation should test both:

1. decode `.bin` into the expected fields;
2. encode the expected fields into the exact `.bin` bytes when the case is
   canonical.

Invalid vectors must be rejected for the reason named by `expected_error`.

Run:

```bash
python scripts/dev/validate-repo.py
```

to verify vector metadata and binary hashes.
