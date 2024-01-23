# Dead Blog Main Backend
contains:
* blog categories
* blog posts
* blog comments
* auth thingies

>While it is based on fastapi (and fastapi intented to run
microservices), this blog is too small and simple, to get
any advantage from splitting it to microservices. In
other hand, you still can possible split it. May be in
future when add more things will be added to blog, they
will be made as dedicated services.


# TODO
\* **comment deletion**
Give admin possibility to delete comments.
\* **language switch**
Add localization for posts and categories.
\* **email subscibtion**
User can add his email to mailing list per category
(include/exclude categories). It will need some
sort of mailing service that uses site domain name.
\* **media loading**
Give admin convinient way to save media files.
\* **make user accounts usable**
Add **optional** user-comment relation to allow
user delete own comments. Make blog posts be owned by
user and add different roles.


# Deploy
This will be updated soon.
