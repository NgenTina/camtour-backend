import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from '../entities/user.entity';
import { Conversation } from '../entities/conversation.entity';
import { Message } from '../entities/message.entity';

@Injectable()
export class SeedService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
    @InjectRepository(Conversation)
    private conversationRepository: Repository<Conversation>,
    @InjectRepository(Message)
    private messageRepository: Repository<Message>,
  ) {}

  async seedDatabase(): Promise<void> {
    // Clear existing data
    await this.messageRepository.clear();
    await this.conversationRepository.clear();
    await this.userRepository.clear();

    // Create sample users
    const user1 = await this.userRepository.save({
      username: 'john_doe',
      email: 'john@example.com',
    });

    const user2 = await this.userRepository.save({
      username: 'jane_smith',
      email: 'jane@example.com',
    });

    // Create sample conversations
    const conversation1 = await this.conversationRepository.save({
      title: 'First Chat with AI',
      user: user1,
    });

    const conversation2 = await this.conversationRepository.save({
      title: 'Technical Support',
      user: user2,
    });

    // Create sample messages for conversation 1
    await this.messageRepository.save([
      {
        content: 'Hello, how are you?',
        sender: 'user',
        conversation: conversation1,
      },
      {
        content: 'I am doing well, thank you for asking!',
        sender: 'ai',
        conversation: conversation1,
      },
      {
        content: 'Can you help me with my project?',
        sender: 'user',
        conversation: conversation1,
      },
      {
        content: 'Of course! What kind of project are you working on?',
        sender: 'ai',
        conversation: conversation1,
      },
    ]);

    // Create sample messages for conversation 2
    await this.messageRepository.save([
      {
        content: 'I need help with my computer',
        sender: 'user',
        conversation: conversation2,
      },
      {
        content: 'Sure, what seems to be the problem?',
        sender: 'ai',
        conversation: conversation2,
      },
      {
        content: 'It keeps crashing when I open large files',
        sender: 'user',
        conversation: conversation2,
      },
      {
        content: 'Try updating your drivers and checking your RAM',
        sender: 'ai',
        conversation: conversation2,
      },
    ]);

    console.log('Database seeded successfully!');
  }
}
