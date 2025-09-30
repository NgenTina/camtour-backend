import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { SeedService } from './seeds/seed.service';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // Seed the database
  const seedService = app.get(SeedService);
  await seedService.seedDatabase();
  
  await app.listen(3000);
  console.log('Application is running on: http://localhost:3000');
}
bootstrap();