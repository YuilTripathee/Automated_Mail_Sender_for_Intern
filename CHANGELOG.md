# CHANGELOG

## July 13, 2019 Saturday

1. Add confirmation feature for checking attachments and snapshots before importing into mail. Implemented in `html_mail_writer.py` in both minified and extended bot variants, under single codebase.
2. Add and extend `mail_utility.py` to reduce code redundancy of same control flow in both bot variants. Some include `hello()`, `hold_file_import()`, `get_week_name()`, `send_mail()`.
