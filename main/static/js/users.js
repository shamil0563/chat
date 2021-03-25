var domain = 'http://127.0.0.1:8000/'
window.onload = function() {

    var rubricListLoader = new XMLHttpRequest();

    rubricListLoader.open('GET', domain + 'api/users/', true);

    rubricListLoader.send();

    rubricListLoader.onreadystatechange = function() {
        if (rubricListLoader.readyState == 4) {
            if (rubricListLoader.status == 200) {

                var data = JSON.parse(rubricListLoader.responseText);

                var s = '<ul>'
                for (i = 0; i < data.length; i++) {
                    d = data[i];
                    detail_url = '<a href="' + domain + 'api/users/' + d.pk+ '/" class="detail">Вывести</a>';
                    s += '<li>' + d.username + ' (' + d.first_name + ') [' + detail_url +']</li>';
                }
                s += '</ul>'
                list.innerHTML = s;

            }
            else{
                window.alert(rubricListLoader.statusText);
            }
        }
    }



}