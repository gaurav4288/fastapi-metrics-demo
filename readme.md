# FastAPI + Prometheus + Grafana Monitoring Demo

## Setup

### 1. Start FastAPI App

```bash
python3 -m venv my_env_name
source my_env_name/bin/activate

cd app
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Monitoring Stack

```bash
docker-compose up -d
hey -n 1000 -c 10 http://localhost:8000/hello
```

- **Prometheus:** [http://localhost:9090](http://localhost:9090)
- **Grafana:** [http://localhost:3000](http://localhost:3000) (login: `admin` / `admin`)

### 3. Check Metrics in Grafana

- Add Prometheus as a data source (`http://prometheus:9090`)
- Create a dashboard: import `grafana_dashboard.json`
- If you’re on Linux and `host.docker.internal` doesn’t work in `prometheus.yml`, replace it with:
    ```yaml
    - targets: ["172.17.0.1:8000"]
    ```
- Check Prometheus UI: [http://localhost:9090](http://localhost:9090)
    - Go to **Status → Targets**
    - You should see your FastAPI target **UP** ✅
    - If it’s **DOWN**, the target address is wrong.

### 4. Verify FastAPI Exposes Metrics

- Open [http://localhost:8000/metrics](http://localhost:8000/metrics)
- You should see output like:
    ```
    # HELP request_count Total request count
    # TYPE request_count counter
    request_count_total{method="GET",endpoint="/hello"} 123
    ```
- If that works, Prometheus can scrape it.

### 5. Check Raw Data in Prometheus

- Go to: [http://localhost:9090](http://localhost:9090)
- Query: `request_count_total` and `request_latency_seconds_count`

### 6. Simulate Load

```bash
hey -n 1000 -c 10 http://localhost:8000/hello
```

- `-n 1000` → total 1000 requests
- `-c 10` → 10 concurrent requests

You can also run a bigger load (e.g., 5000 requests) to see spikes.

---

## Demo Flow

1. **Show Grafana:**  
   Open your FastAPI Monitoring dashboard.

2. **Show Request Rate Graph:**  
   Watch the graph spike as load comes in.

3. **Show 95th Percentile Latency (p95):**  
   See how response times vary.

---

## Pipeline Overview

- FastAPI app exposes metrics on `/metrics`.
- Prometheus scrapes them every 5s.
- Grafana queries Prometheus and visualizes metrics.
- `hey` generates traffic so you can see metrics change live.

---

## ⚡ Pro Tip

Run `hey` once, then keep Grafana visible as the lines move upward—looks great in a recording!  
You can repeat `hey` multiple times with different loads to show how latency grows