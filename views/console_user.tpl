%if user_login == True:
    {{username}} is logged in.
    <form action="/console/logout" method="post" id="loginform" accept-charset="utf-8">
        <p>
            <input name="submit" type="submit" id="submit" value="Logout">
        </p>
    </form>

    <form action="/console/update" method="post" id="updateform" accept-charset="utf-8">
        <p>
            <input name="submit" type="submit" id="submit" value="Update">
        </p>
    </form>
%else:

<form action="/console/login" method="post" id="loginform" accept-charset="utf-8">
    <h3>Login</h3>
    <p><label for="username">Username</label>
        <input id="username" name="username" type="text" value="" required="true">
    </p>
    <p><label for="password">Password</label>
        <input id="password" name="password" type="password" value="" required="true" >
    </p>
    <p>
        <input name="submit" type="submit" id="submit" value="Login">
    </p>
</form>
