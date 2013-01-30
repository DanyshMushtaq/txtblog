%include header title=config.blog_name + ' | '+item.title

<div class="header">
	<div class="container">
	    <div class="row header-content">
	        <div class="onecol"></div>
	        <div class="sevencol">

	            <h1>{{config.blog_name}}</h1>
                %include menu menu=menu

	        </div>
	        <div class="fourcol last"></div>
	    </div>
	</div>
</div>

<div class="content">
	<div class="container">
	    <div class="row">
            <div class="onecol"></div>
            <div class="sevencol">

                %include show_item item=item

            </div>
            <div class="onecol" style="margin-bottom: 1em;"></div>
            <div class="threecol last">
                %include sidebar posts=posts, sidebar_items=sidebar_items
            </div>
	    </div>


	    <div class="row">
            <div class="onecol"></div>
            <div class="sevencol">

                %include show_comments comments=comments
                %include post_comment item=item

            </div>
            <div class="onecol" style="margin-bottom: 1em;"></div>
            <div class="threecol last">
	        </div>
        </div>
	</div>
</div>


%include footer footer_text = config.footer_text
