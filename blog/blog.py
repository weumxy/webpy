#!/usr/bin/python2.7
#coding=utf-8

import web
import model

urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/new', 'New', 'New',
    '/delete/(\d+)', 'Delete',
    'edit/(\d+)', 'Edit',
)

t_globals = {
    'datestr': web.datestr
}

render = web.template.render('templates/')

class Index:
    
    def GET(self):
        """
        show index page
        """
        posts = model.get_posts()
        return render.index(posts)


class view:
    
    def GET(self, id):
        """
        show single post
        """
        post = model.get_post(int(id))
        return render.view(post)

class New:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull, size=30, description="Post content"),
        web.form.Textarea('content', web.form.notnull, rows=30, cols=80, description="Post Content"),
        web.form.Button('Post entry'),
        )
    
    def GET(self):
        form = self.form()
        return render.new(form)
    
    def POST(self):
        form = self.form
        if not form.validates():
            return render.new(form)
        model.new_post(form.d.title, form.d.cotent)
        raise web.seeother('/')

class Delete:
    
    def POST(self, id):
        model.def_post(int(id))
        raise web.seeother('/')

class Edit:

    def GET(self, id):
        """
        edit posts
        """
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)

    def Post(self, id):
        """
        post posts edit
        """
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother('/')
    
app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()

