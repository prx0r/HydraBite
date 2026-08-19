.PHONY: unit hydra certify demo stop

unit:
	./scripts/smoke.sh

hydra:
	./scripts/start_hydradb.sh

certify:
	./scripts/certify.sh

demo:
	uvicorn demo.app:app --host 127.0.0.1 --port 8080

stop:
	./scripts/stop_hydradb.sh
