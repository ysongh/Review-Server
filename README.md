# Review Server
A server using python with flask

+ **Find all Persons**

GET https://reviewserver.herokuapp.com/person

Result - name, company, tags, description, rating

+ **Add a new person**

POST https://reviewserver.herokuapp.com/person

**Request Body Parameters**

Name | Data Type | Description
--- | ---- | ---
name | string | (Required) Name of the person
company | string | (Required) Company that the person works for
image | string | (Option) URL of the image
tags | string | (Required) Separate each tags by a comma
description | string | (Required) Details of the person
rating | decimal | (Required) Must be between 0.0 to 5.0