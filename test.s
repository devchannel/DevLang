.text

.globl main
main:
# We've found a Declaration of type int with name a
# Pushing register t0 onto the stack
addi $sp, $sp, -4
sw $t0, 0($sp)
li $t0, -5

# Popping register t0 off of stack
lw $t0, 0($sp)
addi $sp, $sp, 4

.globl dong
dong:
# We've found a Declaration of type float with name b
# Pushing register t0 onto the stack
addi $sp, $sp, -4
swc1 $f0, 0($sp)
li.s $f0, 12.5

mov.s $f12, $f0 
li $v0, 2
syscall

# Popping register f0 off of stack
lwc1 $f0, 0($sp)
addi $sp, $sp, 4

li $v0, 10
syscall
