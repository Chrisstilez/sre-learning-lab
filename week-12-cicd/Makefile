.PHONY: test build push deploy pipeline clean

# Run the full pipeline: test → build → push → deploy
pipeline: test build push deploy
	@echo ""
	@echo "=== PIPELINE COMPLETE ==="

test:
	@bash pipeline/test.sh

build:
	@bash pipeline/build.sh

push:
	@bash pipeline/push.sh

deploy:
	@bash pipeline/deploy.sh

clean:
	@echo "=== Cleaning up ==="
	kubectl delete -f k8s/deployment.yaml --ignore-not-found
