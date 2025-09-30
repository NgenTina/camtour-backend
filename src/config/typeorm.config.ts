import { TypeOrmModuleOptions } from '@nestjs/typeorm';

export const typeOrmConfig: TypeOrmModuleOptions = {
  type: 'postgres',
  host: 'localhost',
  port: 5432,
  username: 'postgres',
  password: 'password',
  database: 'chatbot_db',
  entities: [__dirname + '/../**/*.entity{.ts,.js}'],
  synchronize: true, // Note: Don't use synchronize in production
  logging: true,
};