while true
do
    export QUART_DEBUG=1
    source venv/bin/activate
    quart run --port 8080 --host 0.0.0.0
done
