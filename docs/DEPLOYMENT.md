# Setup and Deployment

```bash
git clone https://github.com/rsswethaa/anti-spoofing-system.git
cd anti-spoofing-system
python demo.py
python -m unittest discover -s tests -v
```

Optional database:
```bash
python -c "from src.storage import init_db; init_db('antispoof.db', seed=True)"
```

A production architecture would require trusted camera/device ingestion, secure challenge generation, signed session data, model serving, encrypted databases, monitoring and fail-safe authentication policy.
