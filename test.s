.text

.globl main
main:
# We've found a Declaration of type int with name a
# Pushing register t0 onto the stack
addi $sp, $sp, -4
sw $t0, 0($sp)
