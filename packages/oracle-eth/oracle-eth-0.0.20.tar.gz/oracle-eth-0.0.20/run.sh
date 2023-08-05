#!/bin/bash
NAME="army"
cd /HC/GIT/oracle-eth/
source ./venv/bin/activate
#exec $1
#exec army          # 军队
#exec organization  # 事务部
#exec impevent      # 导出event到数据库中

exec python3 $1
#exec python3 run_army.py    # 军队
#exec python3 run_org.py     # 事务部
