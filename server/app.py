from flask import jsonify, make_response
from config import app, api
from models import Post, Comment
from flask_restful import Resource
from sqlalchemy import func

# create routes here:

class ListPosts(Resource):
  
  def get(self):

    posts = Post.query.order_by('title').all()
    return make_response(jsonify([post.to_dict() for post in posts]), 200)

api.add_resource(ListPosts, '/sorted_posts', endpoint='sortedposts')


class AuthorPosts(Resource):

  def get(self, author_name):
    
    post = [post.to_dict() for post in Post.query.filter(Post.author == author_name)]
    return make_response(jsonify(post), 200)

api.add_resource(AuthorPosts, '/posts_by_author/<string:author_name>', endpoint='authorposts')


class SearchPosts(Resource):

  def get(self, title):

    posts = [post.to_dict() for post in Post.query.filter(Post.title.contains(title))]
    return make_response(jsonify(posts), 200)

api.add_resource(SearchPosts, '/search_posts/<string:title>')


class OrderedByComments(Resource):
  
  def get(self):

    posts = Post.query.join(Comment, Post.id == Comment.post_id).group_by(Post.id).order_by(func.count(Comment.id).desc()).all()
    posts_data = [post.to_dict() for post in posts]
    return make_response(jsonify(posts_data), 200)

api.add_resource(OrderedByComments, '/posts_ordered_by_comments')


class MostPopularCommenter(Resource):

  def get(self):

    commenter = Comment.query \
      .with_entities(Comment.commenter, func.count(Comment.id)) \
      .group_by(Comment.commenter) \
      .order_by(func.count(Comment.id).desc()) \
      .first()

    return make_response(jsonify({'commenter': commenter[0]}), 200)
  
api.add_resource(MostPopularCommenter, '/most_popular_commenter')

if __name__ == "__main__":
  app.run(port=5555, debug=True)