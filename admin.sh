#!/bin/zsh

source ~/.zshrc

cleanup() {
    ports=(4000,8005)

    for port in "${ports[@]}"; do
        pid=$(lsof -i :"$port" | awk 'NR==2 {print $2}')

        # Check if the PID is not empty before using it
        if [ -n "$pid" ]; then
            echo "Found PID $pid for port $port. Killing the process..."
            kill -9 "$pid"
        fi
    done
}

cleanup


cd /Users/yangwoolee/repo/captured/admin/frontend
yarn dev --port 4000 &

cd /Users/yangwoolee/repo/captured/admin/backend
pyenv activate py310-admin

python main.py




