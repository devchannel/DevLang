.text

.globl main
main:
# We've found a Declaration of type int with name a
addi $sp, $sp, -4
sw $t0,0($sp)
li $t0, -5

# Pushing register t1 off of stack
lw $t1, 0($sp)
addi $sp, $sp, 4


.globl dong
dong:
# We've found a Declaration of type int with name b
addi $sp, $sp, -4
sw $t0,0($sp)
li $t0, 12

# Pushing register t1 off of stack
lw $t1, 0($sp)
addi $sp, $sp, 4

li $v0, 10
syscall
