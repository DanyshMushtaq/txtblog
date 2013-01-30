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

                %include show_static_item item=item

            </div>
            <div class="onecol"></div>
            <div class="threecol last">

                %include sidebar posts=posts, sidebar_items=sidebar_items

	        </div>
	    </div>
	</div>
</div>


%include footer footer_text = config.footer_text
