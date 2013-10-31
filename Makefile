current: default

default:
	@echo "make [hello|ls]"

check:
	./checklist.py

tree:
	./treelist.py

hello:
	./main.py echo -e "\x1b[31;1;4mHello tkinter\x1b[0m\nThis is the output of \"\x1b[34;3mecho -e\x1b[0m\"."

run:
	./main.py ${COMMAND}

file:
	./main.py cat ${FILE}

ls:
	./main.py ls --color=always
