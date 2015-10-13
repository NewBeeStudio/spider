# Current Problems:

1. One may get failure when crawling, when start again, how to prevent crawled url being crawled again?
- may be done with database -> store, compare, add.
- or use Job Directory provided by scrapy. 
	- need some time to shut down gracefully.
2. Note: current structure of traversing through pages may have some inconvinences! 
   How about revision?
3. Get blocked if crawling too fast. But not the kind of 404/403...
   Not sure whether blocked by ip or cookie or something else.
   How to deal with that?
   