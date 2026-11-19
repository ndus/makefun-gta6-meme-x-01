// Validation for the address POST.json hands in.
//
// The gate reads the post back from X, so a POST.json that names anything
// other than one public post's address can only ever be refused. This module
// checks the address before main.ts copies the file on: the JSON must be an
// object with a string `url`, and the url must be the address of a single
// post on X — an http(s) address on x.com or twitter.com whose path is
// /<handle>/status/<post id>, with nothing after it but an optional
// /photo/<n> or /video/<n> segment, which is still the same post.
//
// The check is pure string work: no network, no clock, no files, so the two
// graded runs of the entry see exactly the same result.

export interface PostAddress {
  handle: string;
  statusId: string;
}

const POST_HOSTS = new Set([
  'x.com',
  'www.x.com',
  'twitter.com',
  'www.twitter.com',
  'mobile.twitter.com',
]);

export function parsePostAddress(raw: string): PostAddress {
  let url: URL;
  try {
    url = new URL(raw);
  } catch {
    throw new Error(`POST.json url is not a valid address: ${JSON.stringify(raw)}`);
  }
  if (url.protocol !== 'https:' && url.protocol !== 'http:') {
    throw new Error(`POST.json url must be http(s), got ${url.protocol}`);
  }
  if (!POST_HOSTS.has(url.hostname)) {
    throw new Error(`POST.json url must be on x.com or twitter.com, got ${url.hostname}`);
  }
  const parts = url.pathname.split('/').filter((part) => part.length > 0);
  if (parts.length < 3 || parts[1] !== 'status') {
    throw new Error(`POST.json url path must be /<handle>/status/<id>, got ${url.pathname}`);
  }
  const [handle, , statusId, ...rest] = parts;
  if (!/^[A-Za-z0-9_]{1,15}$/.test(handle)) {
    throw new Error(`POST.json url handle is not an X handle: ${JSON.stringify(handle)}`);
  }
  if (!/^\d{5,25}$/.test(statusId)) {
    throw new Error(`POST.json url status id must be 5 to 25 digits, got ${JSON.stringify(statusId)}`);
  }
  if (rest.length > 0 && !(rest.length === 2 && (rest[0] === 'photo' || rest[0] === 'video') && /^\d+$/.test(rest[1]))) {
    throw new Error(`POST.json url names more than the post itself: ${url.pathname}`);
  }
  return { handle, statusId };
}

export function readPostAddress(jsonText: string): PostAddress {
  let data: unknown;
  try {
    data = JSON.parse(jsonText);
  } catch {
    throw new Error('POST.json is not valid JSON');
  }
  if (typeof data !== 'object' || data === null || Array.isArray(data)) {
    throw new Error('POST.json must be a JSON object');
  }
  const url = (data as { url?: unknown }).url;
  if (typeof url !== 'string' || url.length === 0) {
    throw new Error('POST.json must carry the post address as a string in "url"');
  }
  return parsePostAddress(url);
}
