const STEP = 6;          // Load more 한 번에 몇 개씩
const FIRST = {};            // 섹션별 처음 보여줄 개수 (기본 STEP)

const LABEL = {
  monthly: '스파크랩 월간호',
  insight: '스파크랩만의 인사이트',
  event: '행사·데모데이',
  program: '프로그램·모집',
};

const state = {}; // { [cat]: shownCount }
let all = [];

function rows(cat) {
  return cat === 'all' ? all : all.filter((a) => a.category === cat);
}

function card(a) {
  const el = document.createElement('a');
  el.className = `card card--${a.category}`;
  el.href = a.url;                       // 스티비 원문으로 이동
  el.target = '_blank';
  el.rel = 'noopener';

  const chip = document.createElement('span');
  chip.className = 'chip';
  chip.textContent = LABEL[a.category];

  const t = document.createElement('strong');
  t.className = 'card__t';
  t.textContent = a.title;               // 따옴표·꺾쇠가 깨지지 않게 textContent

  const [y, m, d] = a.date.split('-');
  const time = document.createElement('time');
  time.className = 'card__d';
  time.dateTime = a.date;
  time.textContent = `${y}/${m}/${d}`;

  el.append(chip, t, time);
  return el;
}

function paint(cat) {
  const grid = document.querySelector(`[data-grid="${cat}"]`);
  const more = document.querySelector(`[data-more="${cat}"]`);
  const list = rows(cat);
  const want = state[cat];

  grid.innerHTML = '';
  list.slice(0, want).forEach((a) => grid.appendChild(card(a)));

  if (!list.length) {
    grid.innerHTML = '<p class="empty">아직 이 주제의 글이 없어요.</p>';
  }
  more.hidden = want >= list.length;
}

function init() {
  document.querySelectorAll('[data-grid]').forEach((g) => {
    const cat = g.dataset.grid;
    state[cat] = FIRST[cat] || STEP;
    paint(cat);
  });

  document.querySelectorAll('[data-more]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const cat = btn.dataset.more;
      state[cat] += STEP;
      paint(cat);
    });
  });
}

// no-cache: 새 호를 올렸을 때 방문자가 옛 목록을 보지 않도록 매번 서버에 확인한다
fetch('articles.json', { cache: 'no-cache' })
  .then((r) => r.json())
  .then((d) => {
    all = d;
    init();
  })
  .catch(() => {
    document.getElementById('main').insertAdjacentHTML(
      'afterbegin',
      '<p class="empty">목록을 불러오지 못했어요.</p>'
    );
  });
