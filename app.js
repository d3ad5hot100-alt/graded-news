// ====================================
// GradEd Study Abroad News
// ====================================

// Sample News Data
// Later replaced automatically by news.json

let newsData = [];

// ====================================

const newsContainer =
    document.getElementById("newsContainer");

const searchInput =
    document.getElementById("searchInput");

const filterButtons =
    document.querySelectorAll(".filter-btn");

const modal =
    document.getElementById("contentModal");

const closeBtn =
    document.querySelector(".close-btn");

// ====================================

function renderNews(newsItems){

    newsContainer.innerHTML = "";

    if(newsItems.length === 0){

        newsContainer.innerHTML = `
        <p>No news found.</p>
        `;

        return;
    }

    newsItems.forEach(news => {

        const card = document.createElement("div");

        card.className = "news-card";

        card.innerHTML = `

        <div class="news-content">

            <div class="news-title">
                ${news.title}
            </div>

            <div class="news-meta">
                ${news.source} • ${news.date}
            </div>

            <div class="news-description">
                ${news.description}
            </div>

            <div class="card-buttons">

                <a
                    href="${news.url}"
                    target="_blank"
                    class="read-btn"
                >
                    Read Article
                </a>

                <button
                    class="content-btn"
                    onclick="generateContent('${encodeURIComponent(news.title)}','${encodeURIComponent(news.description)}')"
                >
                    Content Studio
                </button>

            </div>

        </div>

        `;

        newsContainer.appendChild(card);

    });

}

// ====================================

function generateContent(title, description){

    title = decodeURIComponent(title);
    description = decodeURIComponent(description);

    const summary =
`${description}

This update may affect students planning their study abroad journey. Applicants should review the latest requirements and timelines before making decisions.`;

    const caption =
`🎓 STUDY ABROAD UPDATE

${title}

${description}

Stay informed with the latest international education updates from GradEd Study Abroad News.

#StudyAbroad #InternationalStudents #GradEd`;

    const headline =
title.length > 70
? title.substring(0,70) + "..."
: title;

    document.getElementById(
        "summaryOutput"
    ).innerText = summary;

    document.getElementById(
        "captionOutput"
    ).innerText = caption;

    document.getElementById(
        "headlineOutput"
    ).innerText = headline;

    modal.style.display = "block";
}

// ====================================

closeBtn.onclick = () => {

    modal.style.display = "none";

};

window.onclick = (event) => {

    if(event.target === modal){

        modal.style.display = "none";
    }

};

// ====================================

searchInput.addEventListener(
    "input",
    function(){

        const query =
            this.value.toLowerCase();

        const filtered =
            newsData.filter(item =>

                item.title.toLowerCase()
                    .includes(query)

                ||

                item.description.toLowerCase()
                    .includes(query)

                ||

                item.source.toLowerCase()
                    .includes(query)

            );

        renderNews(filtered);

    }
);

// ====================================

filterButtons.forEach(button => {

    button.addEventListener(
        "click",
        () => {

            filterButtons.forEach(btn =>
                btn.classList.remove("active")
            );

            button.classList.add("active");

            const filter =
                button.dataset.filter;

            if(filter === "all"){

                renderNews(newsData);

                return;
            }

            const filtered =
                newsData.filter(news =>

                    news.category === filter
                    ||
                    news.region === filter

                );

            renderNews(filtered);

        }
    );

});

// ====================================

document.getElementById(
    "refreshNewsBtn"
).addEventListener(
    "click",
    () => {

        alert(
            "Live refresh will be connected in Phase 2 using GitHub Actions."
        );

    }
);

// ====================================

async function loadNews() {

    try {

        const response =
            await fetch("data/news.json");

        newsData =
            await response.json();

        renderNews(newsData);

    }

    catch(error) {

        console.error(error);

    }

}

loadNews();
