import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { typeOrmConfig } from './config/typeorm.config';
import { User } from './entities/user.entity';
import { Conversation } from './entities/conversation.entity';
import { Message } from './entities/message.entity';
import { UserService } from './services/user.service';
import { ConversationService } from './services/conversation.service';
import { MessageService } from './services/message.service';
import { UserController } from './controllers/user.controller';
import { ConversationController } from './controllers/conversation.controller';
import { MessageController } from './controllers/message.controller';
import { SeedModule } from './seeds/seed.module';

@Module({
  imports: [
    TypeOrmModule.forRoot(typeOrmConfig),
    TypeOrmModule.forFeature([User, Conversation, Message]),
    SeedModule,
  ],
  controllers: [
    UserController,
    ConversationController,
    MessageController,
  ],
  providers: [
    UserService,
    ConversationService,
    MessageService,
  ],
})
export class AppModule {}