<div class="side-item">
    %for i in sidebar_items:
        {{!i.html}}
    %end
</div>

<div class="side-item">
    <h2>Recent posts</h2>
    %for p in posts[:5]:
        %item_title = p.title.replace(' ', '+')
        <a href="/blog/{{item_title}}">{{!p.title}}</a><br/>
    %end
</div>

