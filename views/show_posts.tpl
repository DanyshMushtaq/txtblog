%for p in posts:
	<div class="item">
        % item_title = p.title.replace(' ', '+')
		<a href="/blog/{{item_title}}"><h1>{{!p.title}}</h1></a>

		{{!p.html}}

		<div class="post-meta">
            Posted on {{p.date}}
            % if len(p.categories) > 0:
                | categories:
                %for c in p.categories:
                    {{c}}
                %end
            %end
            % if p.comment_count < 1:
            | <a href="/blog/{{item_title}}#comments">Leave a comment</a>
            % elif p.comment_count == 1:
            | <a href="/blog/{{item_title}}#comments">1 comment</a>
            % else:
            | <a href="/blog/{{item_title}}#comments">{{p.comment_count}} comments</a>
            % end
        </div>

	</div>
%end

%if pages > 1:
    %if page < pages:
        <a href="/blog/page/{{page+1}}">Previous</a>
    %end

    %if page > 1:
        <a href="/blog/page/{{page-1}}">Next</a>
    %end
%end

%if pages == 0:
    <p>This blog is empty.</p>
%end