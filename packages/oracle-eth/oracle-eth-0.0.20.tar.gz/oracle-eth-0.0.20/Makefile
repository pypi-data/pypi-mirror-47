PWD = $(shell pwd)

.PHONY: upload config
# 生成 pypi 的发布包，并且发布到 www.pypi.org
upload:
	@echo PWD: $(PWD)
	@cd $(PWD); source $(PWD)/venv/bin/activate
	@python3.6 setup.py sdist build
	twine upload --verbose dist/* && rm -rf ./dist/*

# 将配置文件拷贝到 /etc 目录
config:
	@cp oracle_army.cfg /etc/
	@cp oracle_org.cfg /etc/
