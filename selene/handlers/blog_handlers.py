# -*- coding: utf-8 *-*
import datetime
import tornado.web

from selene import helpers
from selene.handlers import BaseHandler
from tornado.options import options


class HomeHandler(BaseHandler):

    def get(self):
        self.render("home.html", posts=self.application.db.posts.find())


class NewPostHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('newpost.html', message='', post={})

    @tornado.web.authenticated
    def post(self):
        slug_flag = self.get_argument('slug', False)
        if slug_flag:
            slug = self.get_argument('customslug', '')
        else:
            slug = helpers.get_slug(self.get_argument('title'))
        post = {
            'title': self.get_argument('title'),
            'slug': slug,
            'date': datetime.datetime.now(),
            'tags': self.get_argument('tags').split(','),
            'content': self.get_argument('content'),
            'status': self.get_argument('status')
        }
        self.db.posts.insert(post)
        self.redirect('/%s' % post['slug'])


class PostHandler(BaseHandler):

    def get(self, slug_post):
        self.write("Post " + slug_post)


class EditPostHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.write("EditPost")


class DeletePostHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.write("DeletePost")


class RssHandler(BaseHandler):

    def get(self):
        self.set_header("Content-Type", "text/xml; charset=UTF-8")
        self.render("rss.xml",
            posts=self.application.db.posts.find().sort("pubdate",
                -1).limit(10),
            options=options)
