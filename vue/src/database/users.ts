export interface MockUser {
  id: string
  name: string
  email: string
  password: string // 直接存明文仅用于演示，勿用于生产环境
  avatar?: string
  role?: string
  organization?: string
  lastActiveAt?: string
}

export const mockUsers: MockUser[] = [
  {
    id: 'u-1001',
    name: 'Ada Lovelace',
    email: 'ada@example.com',
    password: 'qslp1234',
    avatar: 'https://i.pravatar.cc/120?img=5',
    role: '首席算法设计师',
    organization: '蒸汽时代实验室',
    lastActiveAt: '2025-09-12T09:42:00+08:00',
  },
  {
    id: 'u-1002',
    name: 'Alan Turing',
    email: 'alan@example.com',
    password: 'securepass',
    avatar: 'https://i.pravatar.cc/120?img=15',
    role: '密码分析顾问',
    organization: '布莱切利学院',
    lastActiveAt: '2025-09-18T22:17:00+08:00',
  },
  {
    id: 'u-1003',
    name: 'Grace Hopper',
    email: 'grace@example.com',
    password: 'navyrocks',
    avatar: 'https://i.pravatar.cc/120?img=47',
    role: '编译器先驱',
    organization: '联合舰队学院',
    lastActiveAt: '2025-09-26T15:08:00+08:00',
  },
  {
    id: 'u-1004',
    name: 'Katherine Johnson',
    email: 'katherine@example.com',
    password: 'apollo11',
    avatar: 'https://i.pravatar.cc/120?img=36',
    role: '轨道计算专家',
    organization: '晴空航天中心',
    lastActiveAt: '2025-09-30T08:54:00+08:00',
  },
]
