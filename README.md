* 2015-10-03 Login is finished. Each access should use the self.cookie.[YGH]
* 2015-10-24 UI Updated; Simple analysis of data added; Remove function via website implemented! 
  p.s. Database schema has changed, please drop the stale one and execute "zuoyehezi/createDatabase.sql" 
  **Please put images under the folder "visual/website/website/static/image"**
 * To use Django, you may need to execute:
 * cd visual/website
 * python manage.py makemigrations
 * python manage.py migrate
 * python manage.py runserver
* 2015-10-31 Analysis updated. Enable to ignore the HTML format and parse the options like 'A.', 'A)', or generally 'A*'.
* 2015-11-02 Add "Description", Change type's number into text.