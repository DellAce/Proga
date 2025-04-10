.include "my-macro"	# подключение файла с макроопределениями

.text
        
.global _start
_start:	
        movl $5, %eax # кладем 5 в eax
	movl $1, %ebx # 1 в ebx

L1: 	
        cmpl  $0, %eax # сравниваем eax и 0
	je    L2 # если eax == 0, то jump на Finish
	imull %eax, %ebx # если нет, то идем сюда, и умножаем eax на ebx
	decl  %eax # декремент eax (eax - 1)
	jmp   L1 # всегда переходим на L1 если тут оказались
	
L2:	
        Finish # Finish!!! 
		#"конец работы,
        # возврат в ОС
        # (макро из файла my-macro)"
.end
        
