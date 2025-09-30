import { Controller, Get, Post, Body, Param, Delete, Put, ParseIntPipe } from '@nestjs/common';
import { ConversationService } from '../services/conversation.service';
import { Conversation } from '../entities/conversation.entity';
import { CreateConversationDto } from '../dto/create-conversation.dto';

@Controller('conversations')
export class ConversationController {
  constructor(private readonly conversationService: ConversationService) {}

  @Post()
  async create(@Body() createConversationDto: CreateConversationDto): Promise<Conversation> {
    return await this.conversationService.create(createConversationDto);
  }

  @Get()
  async findAll(): Promise<Conversation[]> {
    return await this.conversationService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id', ParseIntPipe) id: number): Promise<Conversation> {
    return await this.conversationService.findOne(id);
  }

  @Get('user/:userId')
  async findByUserId(@Param('userId', ParseIntPipe) userId: number): Promise<Conversation[]> {
    return await this.conversationService.findByUserId(userId);
  }

  @Put(':id')
  async update(
    @Param('id', ParseIntPipe) id: number,
    @Body('title') title: string
  ): Promise<Conversation> {
    return await this.conversationService.update(id, title);
  }

  @Delete(':id')
  async remove(@Param('id', ParseIntPipe) id: number): Promise<void> {
    return await this.conversationService.remove(id);
  }
}