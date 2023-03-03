import Control.Applicative
import Data.Char

newtype Parser a = Parser {apply :: String -> [(a, String)]}

instance Functor Parser where
    fmap f pa = Parser (\input -> [(f a, rest) | (a, rest) <- apply pa input])

instance Applicative Parser where
    pure a = Parser (\input -> [(a, input)])
    pf <*> pa = Parser (\input -> [(f a, resta) | (f, restf) <- apply pf input, (a, resta) <- apply pa restf])

instance Monad Parser where
    pa >>= k = Parser (\input -> [(b, restb) | (a, resta) <- apply pa input, (b, restb) <- apply (k a) resta])

instance Alternative Parser where
    empty = Parser (\input -> [])
    p <|> p' = Parser (\input -> apply p input ++ apply p' input)


satisfy :: (Char -> Bool) -> Parser Char
satisfy p = Parser go
    where
        go [] = []
        go (x:xs)
            | p x = [(x, xs)]
            | otherwise = []


anychar :: Parser Char
anychar = Parser go
    where
        go [] = []
        go (x:xs) = [(x, xs)]


char :: Char -> Parser Char
char c = Parser go
    where
        go [] = []
        go (x:xs)
            | x == c = [(x, xs)]
            | otherwise = []


digit :: Parser Char
digit = Parser go
    where
        go [] = []
        go (x:xs)
            | isDigit x = [(x, xs)]
            | otherwise = []


space :: Parser Char
space = Parser go
    where
        go [] = []
        go (x:xs)
            | isSpace x = [(x, xs)]
            | otherwise = []

endOfInput :: Parser ()
endOfInput = Parser go
    where
        go "" = [((), "")]
        go _ = []


parse :: Parser a -> String -> Either String a
parse pa input =
    let res = apply (pa <* endOfInput) input
    in
        if null res then Left "Sirul de intrare nu a fost complet consumat sau parsare ambigua"
        else let [(y, rest)] = res
            in Right y


cifraSemn :: Parser Int
cifraSemn
    = do
        c <- anychar
        d <- digit
        if c == '+' then return (digitToInt d)
        else if c == '-' then return (-1 * (digitToInt d))
        else empty


string :: String -> Parser String
string [] = Parser (\input -> [("", input)])
string (x:xs) =
    do
    c <- anychar
    y <- string xs
    if c /= x then empty
    else
        return ([c] ++ y)


naiveNatural :: Parser Int
naiveNatural =
