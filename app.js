const STEP = 6; // Load more 한 번에 몇 개씩

const LABEL = {
  monthly: '스파크랩 월간호',
  insight: '스파크랩만의 인사이트',
  open: '모집·행사',
};

// 'open' 안의 세부 분류 — 카드 칩과 필터 칩에 쓴다
const SUB_LABEL = {
  batch: '🎓 배치·액셀러레이팅',
  demoday: '📊 데모데이·투자유치',
  session: '🎤 세미나·네트워킹',
  support: '🏛 지원사업·공모',
};
const SUB_ORDER = ['batch', 'demoday', 'session', 'support'];

const state = {};      // { [cat]: 보여줄 개수 }
const subFilter = {};  // { [cat]: sub | null }
let all = [];

function rows(cat) {
  const base = cat === 'all' ? all : all.filter((a) => a.category === cat);
  const sub = subFilter[cat];
  return sub ? base.filter((a) => a.sub === sub) : base;
}

// 세부 분류가 있으면 그걸 보여준다 (칩에는 이모지 제외)
function chipText(a) {
  return a.sub ? SUB_LABEL[a.sub].replace(/^\S+\s/, '') : LABEL[a.category];
}

function card(a) {
  const el = document.createElement('a');
  el.className = `card card--${a.category}`;
  el.href = a.url; // 스티비 원문으로 이동
  el.target = '_blank';
  el.rel = 'noopener';

  const chip = document.createElement('span');
  chip.className = 'chip';
  chip.textContent = chipText(a);

  const t = document.createElement('strong');
  t.className = 'card__t';
  t.textContent = a.title; // 따옴표·꺾쇠가 깨지지 않게 textContent

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

  grid.innerHTML = '';
  list.slice(0, state[cat]).forEach((a) => grid.appendChild(card(a)));
  if (!list.length) {
    grid.innerHTML = '<p class="empty">아직 이 주제의 글이 없어요.</p>';
  }
  more.hidden = state[cat] >= list.length;
}

// 세부 분류 필터 칩 — data-filter 가 있는 섹션에만 만든다
function buildFilter(cat) {
  const host = document.querySelector(`[data-filter="${cat}"]`);
  if (!host) return;

  const inCat = all.filter((a) => a.category === cat);
  const counts = {};
  inCat.forEach((a) => {
    counts[a.sub] = (counts[a.sub] || 0) + 1;
  });

  const mk = (sub, text) => {
    const b = document.createElement('button');
    b.className = 'fchip';
    b.type = 'button';
    b.textContent = text;
    b.setAttribute('aria-pressed', String(subFilter[cat] === sub));
    b.addEventListener('click', () => {
      subFilter[cat] = sub;
      state[cat] = STEP; // 필터를 바꾸면 처음부터 6개
      [...host.children].forEach((c) => c.setAttribute('aria-pressed', 'false'));
      b.setAttribute('aria-pressed', 'true');
      paint(cat);
    });
    return b;
  };

  host.appendChild(mk(null, `전체 ${inCat.length}`));
  SUB_ORDER.forEach((s) => {
    if (counts[s]) host.appendChild(mk(s, `${SUB_LABEL[s]} ${counts[s]}`));
  });
}

function init() {
  document.querySelectorAll('[data-grid]').forEach((g) => {
    const cat = g.dataset.grid;
    state[cat] = STEP;
    subFilter[cat] = null;
    buildFilter(cat);
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
