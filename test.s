.text

.globl main
main:
# We've found a Declaration of type int with name a
# Pushing register $t0 onto the stack
addi $sp, $sp, -4
sw $t0, 0($sp)
li $t0, -5

# Popping register t0 off of stack
lw $t0, 0($sp)
addi $sp, $sp, 4
.globl dong
dong:
# We've found a Declaration of type int with name b
# Pushing register $t0 onto the stack
addi $sp, $sp, -4
sw $t0, 0($sp)
li $t0, 12

# Popping register t0 off of stack
lw $t0, 0($sp)
addi $sp, $sp, 4
li $v0, 10
syscall
