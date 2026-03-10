(begin
(define (map func link)
    (if (equal? (length link) 0)
    () (cons (func (car link)) (map func (cdr link)))
    ))

(define (filter func link)
(if (equal? (length link) 0)
() (if (func (car link)) (cons (car link) (filter func (cdr link)))
 (filter func (cdr link)))))


 (define (reduce func link val)
    (if (equal? (length link) 0) val 
    (reduce func (cdr link) (func val (car link)))))
)