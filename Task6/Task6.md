Index updated at 2026-02-14, 2 files added, 0 errors.
Chunks added: 44, Total chunks: 1273

Скрипт для периодического запуска:
crontab -l | { cat; echo "0 4 * * * /...../update-index.py"; } | crontab -


