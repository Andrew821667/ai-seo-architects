#!/usr/bin/env python3
"""
Скрипт инициализации пользователей по умолчанию в PostgreSQL
Создает admin, manager, operator пользователей если их нет в базе
"""

import asyncio
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from api.database.connection import get_db_connection
from api.database.models import User as UserModel


# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Хешировать пароль"""
    return pwd_context.hash(password)


# Пользователи по умолчанию
DEFAULT_USERS = [
    {
        "id": uuid.uuid4(),
        "username": "admin",
        "email": "admin@ai-seo-architects.com",
        "full_name": "System Administrator",
        "password_hash": get_password_hash("secret"),
        "role": "admin",
        "permissions": [
            "agents:read", "agents:write", "agents:delete",
            "campaigns:read", "campaigns:write", "campaigns:delete",
            "clients:read", "clients:write", "clients:delete",
            "analytics:read", "system:admin"
        ],
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": uuid.uuid4(),
        "username": "manager",
        "email": "manager@ai-seo-architects.com",
        "full_name": "SEO Manager",
        "password_hash": get_password_hash("secret"),
        "role": "manager",
        "permissions": [
            "agents:read", "agents:write",
            "campaigns:read", "campaigns:write",
            "clients:read", "clients:write",
            "analytics:read"
        ],
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": uuid.uuid4(),
        "username": "operator",
        "email": "operator@ai-seo-architects.com", 
        "full_name": "SEO Operator",
        "password_hash": get_password_hash("secret"),
        "role": "operator",
        "permissions": [
            "agents:read",
            "campaigns:read",
            "clients:read",
            "analytics:read"
        ],
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


async def init_default_users():
    """Инициализация пользователей по умолчанию в PostgreSQL"""
    print("🚀 Инициализация пользователей по умолчанию...")
    
    try:
        async with get_db_connection() as db:
            created_count = 0
            
            for user_data in DEFAULT_USERS:
                # Проверяем существование пользователя
                result = await db.execute(
                    select(UserModel).where(UserModel.username == user_data["username"])
                )
                existing_user = result.scalar_one_or_none()
                
                if existing_user:
                    print(f"   ⚠️  Пользователь {user_data['username']} уже существует")
                    continue
                
                # Создаем нового пользователя
                new_user = UserModel(**user_data)
                db.add(new_user)
                created_count += 1
                
                print(f"   ✅ Создан пользователь: {user_data['username']} ({user_data['role']})")
            
            # Сохраняем изменения
            if created_count > 0:
                await db.commit()
                print(f"\n🎉 Создано пользователей: {created_count}")
                
                # Показываем учетные данные
                print("\n📋 Учетные данные для входа:")
                print("   Username: admin     | Password: secret | Role: admin")
                print("   Username: manager   | Password: secret | Role: manager")
                print("   Username: operator  | Password: secret | Role: operator")
                print("\n⚠️  ВАЖНО: Смените пароли в production окружении!")
            else:
                print("\n📋 Все пользователи уже инициализированы")
            
    except Exception as e:
        print(f"❌ Ошибка инициализации пользователей: {e}")
        raise


async def check_users_status():
    """Проверить статус пользователей в базе"""
    print("\n📊 Статус пользователей в базе данных:")
    
    try:
        async with get_db_connection() as db:
            result = await db.execute(select(UserModel))
            users = result.scalars().all()
            
            if not users:
                print("   📭 Пользователи не найдены")
                return
            
            print(f"   👥 Всего пользователей: {len(users)}")
            
            for user in users:
                status = "🟢 Активен" if user.is_active else "🔴 Неактивен"
                last_login = user.last_login.strftime("%Y-%m-%d %H:%M") if user.last_login else "Никогда"
                
                print(f"   - {user.username:10} | {user.role:8} | {status} | Вход: {last_login}")
                
    except Exception as e:
        print(f"❌ Ошибка проверки пользователей: {e}")


async def main():
    """Главная функция"""
    print("🔐 AI SEO Architects - Инициализация пользователей")
    print("=" * 60)
    
    try:
        # Инициализируем пользователей
        await init_default_users()
        
        # Проверяем статус
        await check_users_status()
        
        print("\n✅ Инициализация завершена успешно!")
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Прервано пользователем")
        exit(1)
    except Exception as e:
        print(f"\n💥 Неожиданная ошибка: {e}")
        exit(1)