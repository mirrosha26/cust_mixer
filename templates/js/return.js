{% if ts.baner_image != 'baners/default_background.png' and ts.baner_mob_image  != 'baners/default_background.png'   %}

document.addEventListener("DOMContentLoaded", function() {
    // URL изображения для мобильной версии
    var mobileImage = 'media/{{ts.baner_mob_image}}';

    // URL изображения для десктопной версии
    var desktopImage = 'media/{{ts.baner_image}}';

    // Ссылка, куда будет вести баннер
    var link = '{{ts.banner_url}}';

    function insertBanner() {
        var container = document.querySelector(".material-page-container-r-col");

        if (container && container.innerHTML.trim() === '') {
            var windowWidth = window.innerWidth;
            var newContent;

            if (windowWidth <= 450) {
                newContent = `
                    <div style="margin-top: 27px; text-align: center;">
                        <a href="${link}" target="_blank">
                            <img src="${mobileImage}" style="max-width: 98%;" border="0">
                        </a>
                         {% include 'js/social-html.html' %}
                    </div>
                `;
            } else if (windowWidth > 1000) {
                newContent = `
                    <div style="margin-left: 27px; margin-top: 7px;">
                        <a href="${link}" target="_blank">
                            <img src="${desktopImage}" style="max-width: 300px;" border="0">
                        </a>
                            {% include 'js/social-html.html' %}
                    </div>
                `;
            } else {
                newContent = '';
            }

            container.innerHTML = newContent;
        }
    }

    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            var container = document.querySelector(".material-page-container-r-col");
            if (container && container.innerHTML.trim() === '') {
                insertBanner();
            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });

    window.addEventListener('resize', function() {
        var container = document.querySelector(".material-page-container-r-col");
        if (container && container.innerHTML.trim() === '') {
            insertBanner();
        }
    });

    insertBanner();
});

{% else %}

console.log('{{ user.is_superuser }}')

{% endif %}