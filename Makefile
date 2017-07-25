build:
	git clone --branch 0.7.0 https://github.com/ONSdigital/sdx-common.git
	pip3 install ./sdx-common
	cd .. && pip3 install -I ./sdc-cryptography && cd -
	pip3 install -r requirements.txt
	rm -rf sdx-common

test:
	pip3 install -r test_requirements.txt
	flake8 --exclude ./lib/*
	python3 -m unittest discover tests/

clean:
	rm -rf sdx-common