COPY       START     1000               START OF THE PROGRAM, LOADED INTO MEMORY ADDRESS 1000
FIRST      STL       RETADR             STORE THE RETURN ADDRESS (FOR JSUB) IN RETADR
CLOOP      JSUB      RDREC              JUMP TO SUBROUTINE TO READ A RECORD FROM INPUT
-          LDA       LENGTH             LOAD THE LENGTH OF THE RECORD
-          COMP      #0                 COMPARE THE LENGTH WITH 0
-          JEQ       ENDFIL             IF LENGTH IS 0, IT'S THE END OF THE FILE
-          JSUB      WRREC              OTHERWISE, JUMP TO SUBROUTINE TO WRITE THE RECORD
-          J         CLOOP              JUMP BACK TO CLOOP TO PROCESS NEXT RECORD
ENDFIL     LDA       EOF                LOAD THE END-OF-FILE MARKER
-          STA       BUFFER             STORE IT IN THE BUFFER
-          LDA       THREE              LOAD THE VALUE 3
-          STA       LENGTH             STORE IT AS THE LENGTH
-          JSUB      WRREC              WRITE THE END-OF-FILE MARKER
-          J         @RETADR            JUMP TO THE RETURN ADDRESS
.
.
.
RETADR     RESW      1                  RESERVE A WORD FOR THE RETURN ADDRESS
LENGTH     RESW      1                  RESERVE A WORD FOR THE RECORD LENGTH
BUFFER     RESB      4096               RESERVE 4096 BYTES FOR THE BUFFER
EOF        BYTE      C'\n'              DEFINE THE END-OF-FILE MARKER
THREE      BYTE      X'03'              DEFINE THE VALUE 3 IN HEXADECIMAL
-          END       FIRST              END OF THE PROGRAM, SPECIFYING FIRST AS THE ENTRY POINT
