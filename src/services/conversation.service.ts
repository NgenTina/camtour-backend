import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Conversation } from '../entities/conversation.entity';
import { CreateConversationDto } from '../dto/create-conversation.dto';
import { User } from '../entities/user.entity';

@Injectable()
export class ConversationService {
  constructor(
    @InjectRepository(Conversation)
    private conversationRepository: Repository<Conversation>,
    @InjectRepository(User)
    private userRepository: Repository<User>,
  ) {}

  async create(createConversationDto: CreateConversationDto): Promise<Conversation> {
    const user = await this.userRepository.findOne({ where: { id: createConversationDto.userId } });
    if (!user) {
      throw new Error('User not found');
    }

    const conversation = new Conversation();
    conversation.title = createConversationDto.title;
    conversation.user = user;
    return await this.conversationRepository.save(conversation);
  }

  async findAll(): Promise<Conversation[]> {
    return await this.conversationRepository.find({
      relations: ['user', 'messages']
    });
  }

  async findOne(id: number): Promise<Conversation> {
    return await this.conversationRepository.findOne({
      where: { id },
      relations: ['user', 'messages']
    });
  }

  async findByUserId(userId: number): Promise<Conversation[]> {
    return await this.conversationRepository.find({
      where: { user: { id: userId } },
      relations: ['messages']
    });
  }

  async update(id: number, title: string): Promise<Conversation> {
    await this.conversationRepository.update(id, { title, updatedAt: new Date() });
    return await this.conversationRepository.findOne({ where: { id } });
  }

  async remove(id: number): Promise<void> {
    await this.conversationRepository.delete(id);
  }
}