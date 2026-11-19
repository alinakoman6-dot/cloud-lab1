import http from 'k6/http';
import { check, sleep } from 'k6';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.2/index.js';

const BASE_URL = __ENV.BASE_URL;
const N = parseInt(__ENV.VUS || '30');

export const options = {
  stages: [
    { duration: '3m', target: N },  // наростання
    { duration: '5m', target: N },  // стале навантаження
    { duration: '2m', target: 0 },  // спад
  ],
  summaryTrendStats: ['min', 'med', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

const JSON_HEADERS = { 'Content-Type': 'application/json' };
const rnd = (n) => 1 + Math.floor(Math.random() * n);

export function setup() {
  const res = http.post(
    `${BASE_URL}/login`,
    JSON.stringify({ username: 'admin', password: 'admin123' }),
    { headers: JSON_HEADERS }
  );
  return { token: res.json('token') };
}

export default function (data) {
  const auth = { Authorization: `Bearer ${data.token}` };

  const get = (name, path) => {
    const res = http.get(`${BASE_URL}${path}`, { headers: auth, tags: { name } });
    check(res, { [`${name} 200`]: (r) => r.status === 200 });
  };

  // 1 запис
  const res = http.post(
    `${BASE_URL}/children`,
    JSON.stringify({
      first_name: `Load${__VU}`,
      last_name: `Test${__ITER}`,
      birth_date: '2021-03-15',
    }),
    { headers: { ...JSON_HEADERS, ...auth }, tags: { name: 'POST /children' } }
  );
  const ok = check(res, { 'POST 201': (r) => r.status === 201 });
  const id = ok ? res.json('id') : 1;

  // 10 читань
  get('GET /children', '/children');
  get('GET /children/{id} (new)', `/children/${id}`);
  get('GET /children/{id}/parents', `/children/${id}/parents`);
  get('GET /children', '/children');
  get('GET /children/{id}', `/children/${rnd(14)}`);
  get('GET /children/{id}/parents', `/children/${rnd(14)}/parents`);
  get('GET /employees', '/employees');
  get('GET /children', '/children');
  get('GET /children/{id} (new)', `/children/${id}`);
  get('GET /children/{id}/parents', `/children/${rnd(14)}/parents`);

  sleep(0.5);
}

export function handleSummary(data) {
  return {
    stdout: textSummary(data, { indent: ' ', enableColors: false }),
    'loadtest/summary.json': JSON.stringify(data, null, 2),
  };
}