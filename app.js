const PAGE = 20;
const LABEL = {
  insight: '성장 인사이트',
  event: '행사·데모데이',
  program: '프로그램·모집',
  news: '스파크랩 뉴스',
};

const listEl = document.getElementById('list');
const countEl = document.getElementById('count');
const moreEl = document.getElementById('more');
const tabs = [...document.querySelectorAll('.tab')];

let all = [];
let cat = 'all';
let shown = 0;

function filtered() {
  return cat === 'all' ? all : all.filter((a) => a.category === cat);
}

function render(reset) {
  const rows = filtered();
  if (reset) {
    listEl.innerHTML = '';
    shown = 0;
  }
  if (!rows.length) {
    listEl.innerHTML = '<li class="empty">아직 이 주제의 글이 없어요.</li>';
    countEl.textContent = '';
    moreEl.hidden = true;
    return;
  }
  const slice = rows.slice(shown, shown + PAGE);
  for (const a of slice) {
    const li = document.createElement('li');
    li.className = 'item';
    const [y, m, d] = a.date.split('-');
    li.innerHTML = `
      <a href="${a.url}" target="_blank" rel="noopener">
        <time datetime="${a.date}">${y}. ${+m}. ${+d}.</time>
        <span class="t"></span>
        <span class="c ${a.category}">${LABEL[a.category]}</span>
      </a>`;
    // 제목은 textContent로 넣어 따옴표·꺾쇠가 깨지지 않게 한다
    li.querySelector('.t').textContent = a.title;
    listEl.appendChild(li);
  }
  shown += slice.length;
  countEl.textContent = `${rows.length}개의 글`;
  moreEl.hidden = shown >= rows.length;
}

tabs.forEach((t) =>
  t.addEventListener('click', () => {
    tabs.forEach((x) => x.setAttribute('aria-selected', String(x === t)));
    cat = t.dataset.cat;
    render(true);
  })
);

moreEl.addEventListener('click', () => render(false));

fetch('articles.json')
  .then((r) => r.json())
  .then((d) => {
    all = d;
    render(true);
  })
  .catch(() => {
    listEl.innerHTML = '<li class="empty">목록을 불러오지 못했어요.</li>';
  });
