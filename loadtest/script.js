import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: __ENV.VUS ? parseInt(__ENV.VUS) : 80,
  duration: '4m',
};

export default function () {
  http.get(`${__ENV.BASE_URL}/`);
  sleep(0.05);
}
