export type User = {
  sub: string;
  nickname?: string;
  name?: string;
  picture?: string;
  updated_at?: string;
  email?: string;
  email_verified?: boolean;
};

export type Notify = {
  message: string;
  status: string;
};

export type Code = {
  title: string;
  description?: string;
  tags?: string[];
  code?: string;
  url?: string;
  sub?: string;
  created_at?: string;
  key?: string;
};
