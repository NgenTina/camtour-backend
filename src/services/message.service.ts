import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Message } from '../entities/message.entity';
import { CreateMessageDto } from '../dto/create-message.dto';
import { Conversation } from '../entities/conversation.entity';

@Injectable()
export class MessageService {
  constructor(
    @InjectRepository(Message)
    private messageRepository: Repository<Message>,
    @InjectRepository(Conversation)
    private conversationRepository: Repository<Conversation>,
  ) {}

  async create(createMessageDto: CreateMessageDto): Promise<Message> {
    const conversation = await this.conversationRepository.findOne({ 
      where: { id: createMessageDto.conversationId } 
    });
    if (!conversation) {
      throw new Error('Conversation not found');
    }

    const message = new Message();
    message.content = createMessageDto.content;
    message.sender = createMessageDto.sender;
    message.conversation = conversation;
    return await this.messageRepository.save(message);
  }

  async findAll(): Promise<Message[]> {
    return await this.messageRepository.find({
      relations: ['conversation', 'conversation.user']
    });
  }

  async findByConversationId(conversationId: number): Promise<Message[]> {
    return await this.messageRepository.find({
      where: { conversation: { id: conversationId } },
      order: { timestamp: 'ASC' }
    });
  }

  async remove(id: number): Promise<void> {
    await this.messageRepository.delete(id);
  }
}