import pandas as pd
import requests
from django.core.paginator import Paginator
from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from posts.serializers import CommentsSerializer, PostsSerializer


class CustomPaginator:
    def __init__(self, results, per_page, my_serializer, my_page, my_url):
        self.results = results
        self.per_page = per_page
        self.my_serializer = my_serializer
        self.my_page = int(my_page) if my_page is not None else 1
        self.url = my_url

    def paginated_response(self):
        p    = Paginator(self.results, self.per_page)
        if self.my_page > p.num_pages:
            return {"error": "That page contains no result."}
        
        page = p.page(self.my_page)
        previous_page = self.url + "?page=%s" % (self.my_page - 1) if self.my_page and self.my_page > 1 else "-"
        next_page     = self.url + "?page=%s" % (self.my_page + 1) if self.my_page < p.num_pages else "-"
        
        return {
            'count': len(self.results),
            'page_size': self.per_page,
            'total_pages': p.num_pages,
            'links': {
                'previous_page' : previous_page,
                'next_page' :  next_page

            },
            'results': self.my_serializer(page.object_list, many=True).data
            
        }

class PostsView(views.APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        page = self.request.query_params.get('page')

        session  = requests.Session()
        response_comments = session.get('https://jsonplaceholder.typicode.com/comments')
        response_posts    = session.get('https://jsonplaceholder.typicode.com/posts')

        # convert reponse data into json
        comments = response_comments.json()
        posts    = response_posts.json()    

        comments_df = pd.DataFrame.from_dict(comments)
        comments_df = comments_df.groupby(by="postId").agg(count=('postId', 'count'))
        
        posts_df = pd.DataFrame.from_dict(posts)
        
        merge_df = posts_df.merge(comments_df, how='left', left_on="id", right_on="postId")
        merge_df['index'] = merge_df.index
        merge_df = merge_df.sort_values(by=['count', 'index'], ascending=[False, True])
        merge_df = merge_df.rename(columns={"id": "post_id", "title": "post_title", "body": 'post_body', "count": "total_number_of_comments"})
        merge_df = merge_df.drop(columns=['userId', 'index'])

        p = CustomPaginator(merge_df.to_dict(orient='records'), 10, PostsSerializer, page, request.path)
        return Response(p.paginated_response())

class CommentsView(views.APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        page = self.request.query_params.get('page')
        postId = self.request.query_params.get('postId')
        id = self.request.query_params.get('id')
        name = self.request.query_params.get('name')
        email = self.request.query_params.get('email')
        body = self.request.query_params.get('body')

        session  = requests.Session()
        response_comments = session.get('https://jsonplaceholder.typicode.com/comments')
        
        # convert reponse data into json
        comments = response_comments.json()
        comments_df = pd.DataFrame.from_dict(comments)

        # filter comments based on parameters
        if postId:
            comments_df = comments_df.loc[comments_df['postId'] == int(postId)]
        if id:
            comments_df = comments_df.loc[comments_df['id'] == int(id)]
        if name:
            comments_df = comments_df.query('name.str.contains("%s")' % name)
        if email:
            comments_df = comments_df.loc[comments_df['email'] == email]
        if body:
            comments_df =  comments_df.query('body.str.contains("%s")' % body)

        p = CustomPaginator(comments_df.to_dict(orient='records'), 10, CommentsSerializer, page, request.path)
        return Response(p.paginated_response())