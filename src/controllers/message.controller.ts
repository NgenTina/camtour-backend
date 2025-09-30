import { Controller, Get, Post, Body, Param, Delete, ParseIntPipe } from '@nestjs/common';
import { MessageService } from '../services/message.service';
import { Message } from '../entities/message.entity';
import { CreateMessageDto } from '../dto/create-message.dto';

@Controller('messages')
export class MessageController {
  constructor(private readonly messageService: MessageService) {}

  @Post()
  async create(@Body() createMessageDto: CreateMessageDto): Promise<Message> {
    return await this.messageService.create(createMessageDto);
  }

  @Get()
  async findAll(): Promise<Message[]> {
    return await this.messageService.findAll();
  }

  @Get('conversation/:conversationId')
  async findByConversationId(
    @Param('conversationId', ParseIntPipe) conversationId: number
  ): Promise<Message[]> {
    return await this.messageService.findByConversationId(conversationId);
  }

  @Delete(':id')
  async remove(@Param('id', ParseIntPipe) id: number): Promise<void> {
    return await this.messageService.remove(id);
  }
}