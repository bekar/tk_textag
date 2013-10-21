current: file

check:
	./checklist.py

tree:
	./treelist.py

default:
	@echo "make [hello|ls]"

hello:
	./main.py echo -e "\x1b[31;1;4mHello tkinter\x1b[0m\nThis is the output of \"\x1b[34;3mecho -e\x1b[0m\"."

run:
	./main.py ${COMMAND}

file:
	#./main.py cat ${FILE}
	./main.py cat file.in

ls:
	./main.py ls --color=always
